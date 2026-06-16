package nebula.engine.runtime

import nebula.analysis.planner.ExecutionPlan
import nebula.common.codec.SignalCodec
import nebula.common.time.LogicalClock
import nebula.domain.events.StreamSegment

final case class RuntimePolicy(maxParallelism: Int, burstThreshold: Int, laneBias: Map[Int, Int])
final case class RuntimePulse(nodeId: String, slot: Int, pressure: Int, checksum: String)

final case class ExecutionRuntime(policy: RuntimePolicy) {
  def activate(plan: ExecutionPlan, segment: StreamSegment): Vector[RuntimePulse] =
    plan.nodes.zipWithIndex.map { case (node, index) =>
      val bias = policy.laneBias.getOrElse(node.lane, 0)
      val pressure = node.estimatedCost + bias + segment.envelopes.size + node.depth * 5
      val checksum = SignalCodec.fingerprint(
        SignalCodec.tokenize(node.causes.mkString(" ") + pressure.toString, s"lane-${node.lane}")
      )
      RuntimePulse(node.id, index % policy.maxParallelism, pressure, checksum.take(64))
    }

  def watermark(anchor: LogicalClock, pulses: Seq[RuntimePulse]): String = {
    val maxPressure = pulses.map(_.pressure).foldLeft(0)(math.max)
    s"${anchor.stamp("runtime")}#$maxPressure#${pulses.size}"
  }
}

object ExecutionRuntime {
  val default: ExecutionRuntime =
    ExecutionRuntime(
      RuntimePolicy(
        maxParallelism = 6,
        burstThreshold = 90,
        laneBias = Map(0 -> 12, 1 -> 7, 2 -> 3, 3 -> 15),
      )
    )
}
