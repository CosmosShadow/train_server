$(document).ready(function() {
	var data = ['A', 'B', 'C', 'D']
	var index = 1

	function reload() {
		// 清空元素后新生成
		$("#sidebar").html('')
		for (var i = 0; i < data.length; i++) {
			the_class = 'nav_no_active'
			if (i == index) {
				the_class = 'nav_active'
			}
			$("#sidebar").append($("<li></li>").append($("<a role='button' class='nav_li'></a>").addClass(the_class).text(data[i]).attr('index', i)))
		}

		// 绑定按钮
		$(".nav_li").click(function(event) {
			index = parseInt($(event.target).attr('index'))
			console.log(index)
			reload()
		});
	}

	reload()
})
