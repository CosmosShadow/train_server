$(document).ready(function() {
	var projects = []
	var index = Cookies.get('index')
	if (index == null) {
		index = 0
	}

	$.getJSON("/data/projects.json", function(result) {
		console.log(result)
		projects = result
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
	}
})
