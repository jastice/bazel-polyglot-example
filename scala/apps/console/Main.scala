package nebula.apps.console

import nebula.simulation.lab.ScenarioLab

object Main {
  def main(args: Array[String]): Unit = {
    val seed = args.headOption.getOrElse("omega")
    val artifact = ScenarioLab.fabricate(seed)

    println(s"seed=$seed")
    println(s"contracts=${artifact.contracts.map(_.id).mkString(",")}")
    println(s"segment-digest=${artifact.segment.digest.take(120)}")
    println(s"graph-nodes=${artifact.graph.nodes.size} graph-edges=${artifact.graph.edges.size}")
    println(s"hottest-plan=${artifact.plan.hottest.map(node => s"${node.id}:${node.estimatedCost}").mkString(" | ")}")
    println(s"scheduler-spine=${artifact.snapshot.spine}")
    println(s"scheduler-hottest-wave=${artifact.snapshot.hottestWave}")
    println(s"scheduler-total-pressure=${artifact.snapshot.totalPressure}")
    println(s"runtime-digest=${ScenarioLab.runtimeDigest(seed)}")
  }
}
