from metagraph import ConcreteType, Wrapper
from metagraph.default_plugins.abstract_types import DataFrame, Graph, WeightedGraph
from .registry import cudf, cugraph

if cudf:
    class CuDFType(ConcreteType, abstract=DataFrame):
        value_class = cudf.DataFrame

    class CuDFEdgeList(Wrapper, abstract=Graph):
        def __init__(self, df, src_label="source", dest_label="destination"):
            self.value = df
            self.src_label = src_label
            self.dest_label = dest_label
            self._assert_instance(df, cudf.DataFrame)
            self._assert(src_label in df, f"Indicated src_label not found: {src_label}")
            self._assert(
                dest_label in df, f"Indicated dest_label not found: {dest_label}"
            )

    class CuDFWeightedEdgeList(CuDFEdgeList, abstract=WeightedGraph):
        def __init__(
            self,
            df,
            src_label="source",
            dest_label="destination",
            weight_label="weight",
        ):
            super().__init__(df, src_label, dest_label)
            self.weight_label = weight_label
            self._assert(
                weight_label in df, f"Indicated weight_label not found: {weight_label}"
            )


if cugraph:
    class CuGraphType(ConcreteType, abstract=Graph):
        value_type = cugraph.DiGraph

    class CuGraphWeighted(Wrapper, abstract=WeightedGraph):
        def __init__(self, graph, weight_label="weight"):
            self.value = graph
            self.weight_label = weight_label
            self._assert_instance(graph, cugraph.DiGraph)
            self._assert(
                weight_label in graph.nodes(data=True)[0],
                f"Graph is missing specified weight label: {weight_label}",
            )
