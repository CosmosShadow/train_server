$(document).ready(function() {
	var projects = []
	var index = Cookies.get('index')
	if (index == null) {
		index = 0
	}

	$.getJSON("/data/projects.json", function(result) {
		projects = result
		if (index > result.length) {
			index = 0
		}
		fresh_nav()
	})

	function fresh_nav() {
		// 清空元素后新生成
		$("#sidebar").html('')
		for (var i = 0; i < projects.length; i++) {
			the_class = 'nav_no_active'
			if (i == index) {
				the_class = 'nav_active'
			}
			project_name = projects[i]['name']
			$("#sidebar").append($("<li></li>").append($("<a role='button' class='nav_li'></a>").addClass(the_class).text(project_name).attr('index', i)))
		}

		// 绑定按钮
		$(".nav_li").click(function(event) {
			index = parseInt($(event.target).attr('index'))
			Cookies.set('index', index, { expires: 7 })
			console.log(index)
			fresh_nav()
		});

		// 刷新右边内容
		fresh_project(projects[index]['id'])
	}
})


function fresh_project(project_id) {
	$.getJSON("/data/project.json?project_id=" + project_id, function(result) {
		heads = result['heads']
		bodys = result['bodys']

		$("#trains").html('')

		console.log(heads)
		console.log(bodys)

		thead = $("<thead></thead>")
		tr = $("<tr></tr>")
		for (var i = 0; i < heads.length; i++) {
			tr.append($("<td></td>").html(heads[i]))
		}
		thead.append(tr)

		tbody = $("<tbody></tbody")
		for (var i = 0; i < bodys.length; i++) {
			body = bodys[i]
			tr = $("<tr></tr>")
			for (var j = 0; j < body.length; j++) {
				tr.append($("<td></td>").html(body[j]))
			}
			tbody.append(tr)
		}

		$("#trains").append(thead)
		$("#trains").append(tbody)
	})
}
