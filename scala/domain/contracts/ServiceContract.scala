package nebula.domain.contracts

import nebula.common.codec.SignalCodec
import nebula.common.time.{LogicalClock, TemporalModel, TemporalWindow}

final case class Capability(name: String, level: Int, qualifiers: Vector[String]) {
  def signature: String = SignalCodec.weave(qualifiers.prepended(name)).take(72)
}

final case class ContractTerm(code: String, window: TemporalWindow, pressure: Int)

final case class ServiceContract(
    id: String,
    owner: String,
    capabilities: Vector[Capability],
    terms: Vector[ContractTerm],
) {
  lazy val capabilityIndex: Map[String, Capability] = capabilities.map(cap => cap.name -> cap).toMap

  def riskProfile(anchor: LogicalClock): Int = {
    val timePressure = terms.count(_.window.contains(anchor)) * 7
    val capabilityPressure = capabilities.map(_.level).sum
    (timePressure + capabilityPressure + owner.length + id.length) % 101
  }
}

object ServiceContract {
  def synthetic(owner: String, nameSeed: String, offset: Int): ServiceContract = {
    val tokens = SignalCodec.tokenize(nameSeed, owner)
    val capabilities = tokens.take(4).zipWithIndex.map { case (token, index) =>
      Capability(
        name = s"${token.raw}_cap_$index",
        level = (token.weight % 9) + 1,
        qualifiers = Vector(owner, token.channel, token.raw, index.toString),
      )
    }
    val windows = capabilities.zipWithIndex.map { case (cap, index) =>
      ContractTerm(
        code = cap.signature.take(16),
        window = TemporalModel.deriveWindow(cap.name, offset + index),
        pressure = cap.level * (index + 2),
      )
    }
    ServiceContract(s"${owner}_$offset", owner, capabilities.toVector, windows.toVector)
  }
}
