/*
 * 容器基于d3库提供绘制的场景,并分发各事件;
 * 各接口实现响应事件,负责数据的获取、缓存,更新绘制.
 *
 * 场景分发如下事件:
 * - 重绘;
 * - 
 */

/*
 * 创建场景
 *
 * scene_id : 场景绑定的标签
 */
function create_scene(scene_id)
{
	_num_max = 50;
	_num_min = 25;
	_num = Math.round((_num_max+_num_min)/2)
}

create_scene("123");

// 初始化图表
function init_chart()
{
	var svg_width = 900;
	var svg_height = 480;
	var margin = {
		"top" : 20, 
		"bottom" : 20, 
		"left" : 50, 
		"right" : 20
	};
		var buf_size = Math.round((svg_width-margin.left-margin.right)/10);
		var buf = new Array(buf_size);
		for(var i=0; i<buf.length; ++i)
		{
			buf[i] = {
				"data" : 0,
				"stamp" : null
			};
		}

		var svg = d3.select("body").append("svg")
			.attr("width", svg_width)
			.attr("height", svg_height);

		var x_scale, x_axis, y_scale, y_axis;

		function set_chart_parameters()
		{
			x_scale = d3.scale.linear()
				.domain([0, buf.length-1])
				.range([0, svg_width-margin.left-margin.right]);
			x_axis = d3.svg.axis()
				.scale(x_scale)
				.orient("bottom")
				.ticks(10)
				.tickFormat(function (i){
					if(buf[i].stamp==null)
						return "";
					return buf[i].stamp.split(" ")[1];
				});
			
			y_scale = d3.scale.linear()
				.domain(d3.extent(buf, function(d){
						return d.data;
					}))
				.range([svg_height-margin.bottom-margin.top, 0]);
			y_axis =d3.svg.axis()
				.scale(y_scale)
				.orient("left")
				.ticks(10);
		}

		set_chart_parameters();
		svg.append("g").attr("class", "x axis")
			.attr("transform","translate("+margin.left+","+(svg_height-margin.bottom)+")")
			.call(x_axis);
		svg.append("g").attr("class", "y axis")
			.attr("transform", "translate("+margin.left+","+margin.top+")")
			.call(y_axis);

		// for further debug
		//var valid_index = function(buffer){
		//	return 0;
		//};
		//var valid_buffer = function(buffer){
		//	return buffer;
		//};

		var valid_index = function(buffer){
			for(var i=0; i<buffer.length; ++i)
				if(buffer[i].stamp!=null)
					return i;
			return null;
		};

		var valid_buffer = function(buffer){
			var idx = valid_index(buffer);
			if(idx==null)
				return [];
			else
				return buffer.slice(idx, buffer.length);
		};

		var line = d3.svg.line()
			.x(function(d, i){
				return margin.left+x_scale(valid_index(buf)+i);
			})
			.y(function(d, i){
				return margin.top+y_scale(d.data);
			});
			//.interpolate('basis');

		// - 添加曲线
		svg.append("path")
			.attr("d", line(valid_buffer(buf)))
			.attr("class", "curve")
			.style("stroke-width", 2)
			.style("stroke", "#000")
			.style("fill", "none");

		// - 描点
		var radius_default = 3, radius_bold = 5;
		var point_x = function(d, i){
			return margin.left+x_scale(i);
		};
		var point_y = function(d, i){
			return margin.top+y_scale(d.data);
		};
		var point_visible = function(d, i){
			if(d.stamp==null)
				return "hidden";
			return "visible";
		};
		svg.selectAll("circle")
			.data(buf)
			.enter().append("circle")
			.attr("cx", function(d,i){
				return point_x(d, i);
			})
			.attr("cy", function(d, i){
				return point_y(d, i);
			})
			.attr("r", radius_default)
			.attr("class", "point")
			.style("fill", "#F00")
			.style("visibility", function(d, i){
				return point_visible(d, i);
			})
			.on("mouseover", function(){
				d3.select(this).transition().duration(100).attr("r", radius_bold);
				var m = d3.mouse(this);
				var x_ind = x_scale.invert(m[0]-margin.left);
				x_ind = Math.round(x_ind);
				d3.select("#tips-stamp").text("时间 : "+buf[x_ind].stamp);
				d3.select("#tips-data").text("数值 : "+buf[x_ind].data.toFixed(2));
				var tips_x=m[0], tips_y=m[1];
				var tips_w = parseInt(d3.select("#tips-border").attr("width"));
				var tips_h = parseInt(d3.select("#tips-border").attr("height"));
				if(tips_x+tips_w>=svg_width)
					tips_x -= tips_w;
				if(tips_y+tips_h>=svg_height)
					tips_y -= tips_h;
				d3.select("#tips")
					.style("display", "block")
					.attr("transform", "translate("+tips_x+","+tips_y+")");
			})
			.on("mouseout", function(){
				d3.select(this).transition().duration(100).attr("r", radius_default);
				d3.select("#tips").style("display", "none");
			});
		
		// - 标签文字
		var tips = svg.append("g")
			.attr("id", "tips");
		tips.append("rect")
			.attr("id", "tips-border")
			.attr("width", 200)
			.attr("height", 100)
			.attr("rx", 10)
			.attr("ry", 10)
			.attr("fill", "#eeeeee");
		tips.append("text")
			.attr("id", "tips-stamp")
			.attr("x", 10)
			.attr("y", 20)
			.text("");
		tips.append("text")
			.attr("id", "tips-data")
			.attr("x", 10)
			.attr("y", 40)
			.text("");
		d3.select("#tips").style("display", "none");

		function redraw_chart(new_data) 
		{
			for(var i=0; i<buf.length-1; ++i)
				buf[i] = buf[i+1];
			buf[buf.length-1] = new_data;

			if(!auto_ref)
				return;

			set_chart_parameters();
			svg.selectAll("g.y.axis").call(y_axis);
			svg.selectAll("g.x.axis").call(x_axis);
			svg.selectAll(".curve")
				.attr("d", line(valid_buffer(buf)));
			
			svg.selectAll(".point")
				.data(buf)
				.attr("cx", function(d,i){
					return point_x(d, i);
				})
				.attr("cy", function(d, i){
					return point_y(d, i);
				})
				.style("visibility", function(d, i){
					return point_visible(d, i);
				});
		}


		function create_mouse_watcher()
		{
			var mouse_pressed = false;
			var mouse_last_down;

			function on_down()
			{
				mouse_pressed = true;
				mouse_last_down = d3.mouse(this);
			}

			function on_up()
			{
				mouse_pressed = false;
				var p = d3.mouse(this);
				var x_dis = p[0]-mouse_last_down[0];
				x_dis += margin.left;
				var x_ind = x_scale.invert(x_dis-margin.left);
				x_ind = Math.round(x_ind);
				if(x_ind>0)
					console.log("->, earlier "+x_ind);
				else if(x_ind<0)
					console.log("<-, later "+(-x_ind));
			}
			
			function on_move()
			{
				if(!mouse_pressed)
					return;
				var m = d3.mouse(this);
				var x_ind = x_scale.invert(m[0]-margin.left);
				x_ind = Math.round(x_ind);
				//console.log(x_ind);
			}

			return {
				"down" : on_down, 
				"up" : on_up, 
				"move" : on_move
			};
		}
		var mouse_watcher = create_mouse_watcher();
		svg.on("mousedown.stock", mouse_watcher.down)
			.on("mouseup.stock", mouse_watcher.up)
			.on("mousemove.stock", mouse_watcher.move);

		return {
			"redraw" : redraw_chart, // 更新曲线
			"ref_flag" : function(){ // 前台是否刷新
				return auto_ref;
			},
			"toggle_ref" : function(){ // 前台刷新切换
				if(auto_ref)
					auto_ref = false;
				else
					auto_ref = true;
			}
		};
	}

	var handle = init_chart();
	var ws_target = window.location.protocol+"//"+window.location.host;
	var socket = io.connect(ws_target);
	socket.on("connect", function(){
		console.log("connected");
	});
	socket.on("disconnect", function(){
		console.log("disconnected");
	});
	socket.on('msg', function (data) {
		//console.log(data);
		handle.redraw(data);
	});

	d3.select("#auto_ref")
		.attr("value", "暂停")
		.on("click", function(){
			handle.toggle_ref();
			if(handle.ref_flag())
				d3.select(this).attr("value", "暂停");
			else
				d3.select(this).attr("value", "恢复");
		});
