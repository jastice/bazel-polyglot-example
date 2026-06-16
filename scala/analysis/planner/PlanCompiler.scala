package nebula.analysis.planner

import nebula.analysis.graph.DependencyGraph
import nebula.common.time.{LogicalClock, TemporalModel}
import nebula.domain.contracts.ServiceContract
import nebula.domain.events.StreamSegment

final case class PlanNode(id: String, lane: Int, depth: Int, estimatedCost: Int, causes: Vector[String])
final case class ExecutionPlan(anchor: LogicalClock, nodes: Vector[PlanNode], diagnostics: Vector[String]) {
  def hottest: Vector[PlanNode] = nodes.sortBy(node => (-node.estimatedCost, node.id)).take(5)
}

object PlanCompiler {
  def compile(
      anchor: LogicalClock,
      contracts: Seq[ServiceContract],
      segment: StreamSegment,
      graph: DependencyGraph,
  ): ExecutionPlan = {
    val contractRisk = contracts.map(contract => contract.id -> contract.riskProfile(anchor)).toMap
    val braided = TemporalModel.braid(contracts.flatMap(_.terms.map(_.window)))

    val nodes = graph.nodes.zipWithIndex.map { case (node, index) =>
      val adjacencyPressure = graph.outboundPressure(node.id)
      val risk = contractRisk.getOrElse(node.id, node.weight % 17)
      val segmentPressure = segment.topicPressure.values.sum
      val widthBias = (braided.width % 23).toInt
      PlanNode(
        id = node.id,
        lane = index % 4,
        depth = graph.adjacency.getOrElse(node.id, Vector.empty).size,
        estimatedCost = node.weight + adjacencyPressure + risk + segmentPressure + widthBias,
        causes = node.labels.take(3),
      )
    }.toVector.sortBy(node => (-node.estimatedCost, node.id))

    val diagnostics = Vector(
      s"segment-digest=${segment.digest.take(96)}",
      s"graph-spine=${graph.renderSpine.take(96)}",
      s"window-width=${braided.width}",
      s"node-count=${nodes.size}",
    )

    ExecutionPlan(anchor, nodes, diagnostics)
  }
}
