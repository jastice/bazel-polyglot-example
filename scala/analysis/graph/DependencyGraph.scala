package nebula.analysis.graph

import nebula.common.codec.SignalCodec
import nebula.domain.contracts.ServiceContract
import nebula.domain.events.EventEnvelope

final case class GraphNode(id: String, weight: Int, labels: Vector[String])
final case class GraphEdge(from: String, to: String, reason: String, pressure: Int)

final case class DependencyGraph(nodes: Vector[GraphNode], edges: Vector[GraphEdge]) {
  lazy val adjacency: Map[String, Vector[GraphEdge]] =
    edges.groupBy(_.from).view.mapValues(_.sortBy(edge => (-edge.pressure, edge.to))).toMap

  def outboundPressure(nodeId: String): Int =
    adjacency.getOrElse(nodeId, Vector.empty).map(_.pressure).sum

  def renderSpine: String =
    nodes.sortBy(node => (-outboundPressure(node.id), node.id)).map(node => s"${node.id}:${node.weight}").mkString(" -> ")
}

object DependencyGraph {
  def assemble(contracts: Seq[ServiceContract], events: Seq[EventEnvelope]): DependencyGraph = {
    val contractNodes = contracts.map { contract =>
      GraphNode(
        id = contract.id,
        weight = contract.capabilities.map(_.level).sum + contract.terms.map(_.pressure).sum,
        labels = contract.capabilities.map(_.name),
      )
    }

    val eventEdges = events.flatMap { event =>
      contracts.find(_.id == event.contractId).toVector.flatMap { contract =>
        contract.capabilities.map { capability =>
          val tokens = SignalCodec.tokenize(capability.signature + event.id, capability.name)
          GraphEdge(
            from = contract.id,
            to = s"${event.topic}_${capability.level}",
            reason = tokens.take(3).map(_.raw).mkString("."),
            pressure = tokens.map(_.weight).sum % 113,
          )
        }
      }
    }

    val syntheticNodes = eventEdges.map(_.to).distinct.sorted.map { id =>
      GraphNode(id = id, weight = id.length * 3, labels = Vector(id.take(5), "synthetic"))
    }

    DependencyGraph((contractNodes ++ syntheticNodes).toVector, eventEdges.toVector)
  }
}
