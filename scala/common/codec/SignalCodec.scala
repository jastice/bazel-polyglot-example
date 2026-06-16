package nebula.common.codec

final case class SignalToken(raw: String, weight: Int, channel: String)

object SignalCodec {
  private val delimiters = "[\\s,;:|]+".r

  def tokenize(input: String, channel: String): Vector[SignalToken] =
    delimiters
      .split(input.trim)
      .iterator
      .filter(_.nonEmpty)
      .zipWithIndex
      .map { case (part, index) =>
        val normalized = part.toLowerCase.replaceAll("[^a-z0-9_\\-]", "")
        val weight = normalized.foldLeft(index + 17)((acc, ch) => acc * 31 + ch.toInt).abs
        SignalToken(normalized, (weight % 97) + 3, channel)
      }
      .toVector

  def fingerprint(tokens: Iterable[SignalToken]): String =
    tokens
      .groupBy(_.channel)
      .toVector
      .sortBy(_._1)
      .map { case (channel, channelTokens) =>
        val magnitude = channelTokens.map(_.weight.toLong).sum
        val shape = channelTokens.map(_.raw.take(3)).mkString("-")
        s"$channel[$magnitude]=$shape"
      }
      .mkString("::")

  def weave(parts: Iterable[String]): String =
    parts.iterator.zipWithIndex.map { case (part, index) => s"${index.toHexString}:${part.reverse}" }.mkString("/")
}
