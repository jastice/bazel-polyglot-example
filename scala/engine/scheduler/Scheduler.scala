package nebula.engine.scheduler

import nebula.analysis.graph.DependencyGraph
import nebula.analysis.planner.ExecutionPlan
import nebula.common.time.TemporalModel
import nebula.domain.events.StreamSegment
import nebula.engine.runtime.{ExecutionRuntime, RuntimePulse}

final case class ScheduledWave(slot: Int, pulses: Vector[RuntimePulse], aggregatePressure: Int)
final case class SchedulerSnapshot(spine: String, hottestWave: Int, totalPressure: Int)

final class Scheduler(runtime: ExecutionRuntime) {
  def schedule(plan: ExecutionPlan, graph: DependencyGraph): Vector[ScheduledWave] = {
    val pulses = runtime.activate(plan, StreamSegment(
      window = TemporalModel.braid(Vector.empty ++ plan.nodes.take(1).map(_ => TemporalModel.deriveWindow("fallback", 1))),
      envelopes = Vector.empty,
    ))
    pulses
      .groupBy(_.slot)
      .toVector
      .sortBy(_._1)
      .map { case (slot, slotPulses) =>
        val graphPressure = slotPulses.map(pulse => graph.outboundPressure(pulse.nodeId)).sum
        ScheduledWave(slot, slotPulses.sortBy(pulse => (-pulse.pressure, pulse.nodeId)), graphPressure + slotPulses.map(_.pressure).sum)
      }
  }

  def snapshot(plan: ExecutionPlan, graph: DependencyGraph): SchedulerSnapshot = {
    val waves = schedule(plan, graph)
    SchedulerSnapshot(
      spine = graph.renderSpine.take(120),
      hottestWave = waves.sortBy(wave => (-wave.aggregatePressure, wave.slot)).headOption.map(_.slot).getOrElse(-1),
      totalPressure = waves.map(_.aggregatePressure).sum,
    )
  }
}

object Scheduler {
  def default: Scheduler = new Scheduler(ExecutionRuntime.default)
}
