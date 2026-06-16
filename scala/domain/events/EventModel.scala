package nebula.domain.events

import nebula.common.codec.SignalCodec
import nebula.common.time.{LogicalClock, TemporalWindow}
import nebula.domain.contracts.ServiceContract

final case class EventEnvelope(
    id: String,
    contractId: String,
    topic: String,
    clock: LogicalClock,
    payload: Map[String, String],
)

final case class StreamSegment(window: TemporalWindow, envelopes: Vector[EventEnvelope]) {
  lazy val topicPressure: Map[String, Int] =
    envelopes.groupBy(_.topic).view.mapValues(_.size).toMap

  def digest: String =
    SignalCodec.fingerprint(
      envelopes.flatMap(env => SignalCodec.tokenize(env.payload.values.mkString(" "), env.topic))
    )
}

object EventModel {
  def fromContracts(contracts: Seq[ServiceContract], baseClock: LogicalClock): Vector[EventEnvelope] =
    contracts.zipWithIndex.flatMap { case (contract, contractIndex) =>
      contract.capabilities.zipWithIndex.map { case (capability, capIndex) =>
        val clock = baseClock.advance(contractIndex * 13 + capIndex * 5)
        EventEnvelope(
          id = s"${contract.id}::${capability.name}",
          contractId = contract.id,
          topic = capability.name.takeWhile(_ != '_'),
          clock = clock,
          payload = Map(
            "signature" -> capability.signature,
            "owner" -> contract.owner,
            "level" -> capability.level.toString,
            "risk" -> contract.riskProfile(clock).toString,
          ),
        )
      }
    }.toVector

  def segmentize(window: TemporalWindow, envelopes: Vector[EventEnvelope]): StreamSegment =
    {
      val inWindow = envelopes.filter(env => window.contains(env.clock))
      StreamSegment(window, if (inWindow.nonEmpty) inWindow else envelopes)
    }
}
