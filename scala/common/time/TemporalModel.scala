package nebula.common.time

final case class LogicalClock(epoch: Long, tick: Long) {
  def advance(by: Int): LogicalClock = copy(tick = tick + by.toLong)
  def stamp(label: String): String = s"$label@$epoch:$tick"
}

final case class TemporalWindow(open: LogicalClock, close: LogicalClock) {
  require(close.tick >= open.tick, "window must not travel backwards")

  def width: Long = close.tick - open.tick
  def contains(clock: LogicalClock): Boolean =
    clock.epoch == open.epoch && clock.tick >= open.tick && clock.tick <= close.tick
}

object TemporalModel {
  def deriveWindow(seed: String, offset: Int): TemporalWindow = {
    val epoch = 2026L + (seed.length % 5)
    val start = seed.foldLeft(11L)(_ + _.toLong) + offset.toLong
    val open = LogicalClock(epoch, start)
    TemporalWindow(open, open.advance(math.max(3, seed.length + offset)))
  }

  def braid(windows: Seq[TemporalWindow]): TemporalWindow = {
    val first = windows.minBy(_.open.tick)
    val last = windows.maxBy(_.close.tick)
    TemporalWindow(first.open.copy(epoch = last.close.epoch), last.close)
  }
}
