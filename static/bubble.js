d3.select("svg").remove();

// Make the pack fit in the browser, accounting for the title (hard coded)
var diameter = Math.min(window.innerWidth, (window.innerHeight - 80));

var format = d3.format(",d"); // used in node title

var color = d3.scale.linear()
    .domain([0, 2, 4])
    .range(["red", "yellow", "green"]);

var div = d3.select("body").append("div") 
    .attr("class", "tooltip")       
    .style("opacity", 0);

// make a bubble, packed, with size and padding
// If I use .force() instead of .pack(), I can make it wiggle
var bubble = d3.layout.pack()
  .sort(null)
  .size([diameter, diameter])
  .padding(3);

// Add an svg element to the body with a width, height, and class
var svg = d3.select(".bubble").append("svg")
  .attr("width", diameter)
  .attr("height", diameter)
  .attr("class", "bubble")
  .attr("class", "center");

// make a server call to get data
d3.json("channel_data.json", function(error, root) {

  if (error) throw error;
  console.log(root);

  // every circle is a node
  var node = svg.selectAll(".node")
    .data(bubble.nodes(root)
    // this filters out any nodes with children (ie the giant circle)
    .filter(function(d) { return !d.children; }))
    // g is the svg element that holds each circle
    .enter().append("g")
    .attr("class", "node")
    // transform determines location, and are calculate by d3
    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"})
    .on("mouseover", function(d) {    
      div.transition()    
          .duration(200)    
          .style("opacity", .9);    
      div .html(d.name + "<br/>"  + "Hello!")  
          .style("left", (d3.event.pageX) + "px")   
          .style("top", (d3.event.pageY - 28) + "px");  
    })          
    .on("mouseout", function(d) {   
      div.transition()    
          .duration(500)    
          .style("opacity", 0); });

  // // add a title to the node
  // node.append("title")
  //   .text(function(d) { return d.name; });

  // add a circle element to the node
  node.append("circle")
    .attr("r", function(d) { return d.r; })
    .attr("class", "bubble")
    .style("fill", function(d) { return color(d.sentiment);});

  // // add name label to the node
  // node.append("text")
  //   .attr("dy", ".3em")
  //   .attr("class", "bubble-text")
  //   .style("text-anchor", "middle")
  //   .text(function(d) { return d.name; });

  // // For each node, include an invisible rectangle for text-wrapping boundaries.
  // // rectangle appears but is in the wrong spot
  // node.append("rect")
  //   .attr('id', function(d){ return "rect"+d.value; })
  //   .attr("x", function(d){ return d.x })
  //   .attr("y", function(d){ return d.y })
  //   .attr("width", function(d) { return (d.r * 2);})
  //   .style("opacity", '0.5') // increased opacity for debugging only
  //   .attr("height", function(d) { return (d.r * 2);});

  // // this should add text so that it wraps?
  // node.append("text")
  //   .attr('id', function(d){ return "text"+d.value; })
  //   .attr("class", "bubble-text")
  //   .attr("dy", ".3em")
  //   .style("text-anchor", "middle")
  //   .text(function(d) {
  //        return d.name.substring(0, d.r / 3);
  //      });
 });

// ??
// d3.select(self.frameElement).style("height", diameter + "px");
