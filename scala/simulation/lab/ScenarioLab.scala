package nebula.simulation.lab

import nebula.analysis.graph.DependencyGraph
import nebula.analysis.planner.{ExecutionPlan, PlanCompiler}
import nebula.common.time.{LogicalClock, TemporalModel}
import nebula.domain.contracts.ServiceContract
import nebula.domain.events.{EventModel, StreamSegment}
import nebula.engine.runtime.ExecutionRuntime
import nebula.engine.scheduler.{Scheduler, SchedulerSnapshot}

final case class ScenarioArtifact(
    contracts: Vector[ServiceContract],
    segment: StreamSegment,
    graph: DependencyGraph,
    plan: ExecutionPlan,
    snapshot: SchedulerSnapshot,
)

object ScenarioLab {
  def fabricate(seed: String): ScenarioArtifact = {
    val anchor = LogicalClock(2028L, seed.length.toLong * 3L + 19L)
    val contracts = Vector(
      ServiceContract.synthetic("atlas", s"$seed ingress lattice mirror", 2),
      ServiceContract.synthetic("borealis", s"$seed settlement switchyard pulse", 5),
      ServiceContract.synthetic("cinder", s"$seed archive relay prism", 8),
      ServiceContract.synthetic("delta", s"$seed sentinel cadence reactor", 11),
    )
    val envelopes = EventModel.fromContracts(contracts, anchor)
    val window = TemporalModel.braid(contracts.flatMap(_.terms.map(_.window)))
    val segment = EventModel.segmentize(window, envelopes)
    val graph = DependencyGraph.assemble(contracts, segment.envelopes)
    val plan = PlanCompiler.compile(anchor, contracts, segment, graph)
    val scheduler = Scheduler.default
    ScenarioArtifact(
      contracts = contracts,
      segment = segment,
      graph = graph,
      plan = plan,
      snapshot = scheduler.snapshot(plan, graph),
    )
  }

  def runtimeDigest(seed: String): String = {
    val artifact = fabricate(seed)
    val runtime = ExecutionRuntime.default
    runtime.watermark(artifact.plan.anchor, runtime.activate(artifact.plan, artifact.segment))
  }
}
