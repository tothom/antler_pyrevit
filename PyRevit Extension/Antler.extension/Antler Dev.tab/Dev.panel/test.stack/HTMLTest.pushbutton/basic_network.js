// <script type="text/javascript" src=".\vis-network.min.js"></script>
// <script type="text/javascript" src="https://unpkg.com/vis-data/standalone/umd/vis-data.min.js"></script>
// <script type="text/javascript" src="https://unpkg.com/vis-util/standalone/umd/vis-util.min.js"></script>

// import './vis-network.min.js'

// create an array with nodes
var nodes = new vis.DataSet([
  { id: 1, label: "Node 1" },
  { id: 2, label: "Node 2" },
  { id: 3, label: "Node 3" },
  { id: 4, label: "Node 4" },
  { id: 5, label: "Node 5" }
]);

// create an array with edges
var edges = new vis.DataSet([
  { from: 1, to: 3 },
  { from: 1, to: 2 },
  { from: 2, to: 4 },
  { from: 2, to: 5 },
  { from: 3, to: 3 }
]);

// create a network
var container = document.getElementById("mynetwork");
var data = {
  nodes: nodes,
  edges: edges
};
var options = {};
var network = new vis.Network(container, data, options);
