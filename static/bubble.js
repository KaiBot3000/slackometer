var diameter = 960,
  format = d3.format(",d"), // used in node title
  // color = d3.scale.category20c(); //used in node color
  color = d3.scale.linear()
    .domain([0, 0.1, 2, 4])
    .range(["gray", "red", "yellow", "green"]);

// make a bubble, packed, with size and padding
var bubble = d3.layout.pack()
  .sort(null)
  .size([diameter, diameter])
  .padding(1.5);

// Add an svg element to the body with a width, height, and class
var svg = d3.select("body").append("svg")
  .attr("width", diameter)
  .attr("height", diameter)
  .attr("class", "bubble");

// make a server call to get data
d3.json("channel_data.json", function(error, root) {
  // error out if no data
  if (error) throw error;
  console.log(root);

  // every circle is a node
  var node = svg.selectAll(".node")
    // .data(bubble.nodes(classes(root))
    .data(bubble.nodes(root)
    // this filters out any nodes with children (ie the giant circle)
    .filter(function(d) { return !d.children; }))
    // g is the svg element that holds each circle
    .enter().append("g")
    // add 'node' class
    .attr("class", "node")
    // transform determines location, and are calculate by d3
    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  // add a title to the node
  node.append("title")
    .text(function(d) { return d.name; });

  // add a circle element to the node
  node.append("circle")
    .attr("r", function(d) { return d.r; })
    .style("fill", function(d) { return color(d.sentiment);});

    // Trying to make empty channels grey, and failing
    // .style("fill", function(d) { 
  //       if (parseInt((d.sentiment) > 0) {
  //         console.log("big");
  //         console.log(typeof(d.sentiment));
  //         return color(d.sentiment);
  //       } else {
  //         console.log("zero");
  //         return  "#D3D3D3";
  //       }});
    // .style("stroke", "black")
      // .style("stroke-width", "-2");

  // For each node, include an invisible rectangle for text-wrapping boundaries.
  // rectangle appears but is in the wrong spot
  node.append("rect")
    .attr('id', function(d){ return "rect"+d.value; })
    .attr("x", function(d){ return d.x })
    .attr("y", function(d){ return d.y })
    .attr("width", function(d) { return (d.r * 2);})
    .style("opacity", '0.5') // increased opacity for debugging only
    .attr("height", function(d) { return (d.r * 2);});

  // add some text to the node (title?)
  // node.append("text")
  //   .attr("dy", ".3em")
  //   .style("text-anchor", "middle")
  //   .text(function(d) { return d.name; });

  // this should add text so that it wraps
  node.append("text")
    .attr('id', function(d){ return "text"+d.value; })
    .attr("dy", ".3em")
    .style("text-anchor", "middle")
    .text(function(d) {
         return d.name.substring(0, d.r / 3);
       });
} );

// ??
d3.select(self.frameElement).style("height", diameter + "px");
