
app.filter('pad', function(){
	return function(num, chars){
		if (num < 1){
			num = 1;
		}
		chars -= Math.ceil(Math.log(num+1)/Math.LN10);
		str = String(num);
		while (chars > 0 && isFinite(chars)){ 
			str = "\xA0" + str;
			chars--;
		}
		return str;
	}
});

app.filter('linefilter', function(){
	return function(str){
		if (str){
			str = str.replace('\t','\xA0\xA0\xA0\xA0');
			return str.replace(' ', '\xA0');
		}
		return "";
	}
});

app.filter('msTime', function(){
    // Negative time denotes failure
	return function(ms){
		if (ms){
            if (ms >= 0) {
                return String(ms.toFixed(3)) + " ms";
            } else {
                return "Lines Ran Exceeded Limit";
            }
		} else {
			return "";
		}
	}
});


var VisualizerController = 
	   ['$scope','$window','$timeout',
function($scope , $window , $timeout){
	S = $scope;
	$scope.data = $window.data;
	$scope.lineCount = $scope.data.code.length;
	$scope.lineNumDigits = Math.ceil(Math.log($scope.lineCount + 1)/Math.LN10);
	$scope.mouseover = [];
	$scope.frequencies = Array.apply(null, new Array($scope.lineCount)).map(Number.prototype.valueOf,0);
	$scope.max_frequency = 1;

	$timeout(function(){
		var branches = $scope.data.branches;
		var curr = 1;
		var next;
		for (var i=0; i<branches.length; i++){
			next = branches[i][0];
			while (curr != next){
				$scope.execute(curr);
				curr++;
			}
			curr = branches[i][1];
			$scope.execute(curr);
		}
		for (var i=1; i<$scope.lineCount; i++){
			document.getElementById(String(i)).style.stroke = lineColor(i);
		}

		$scope.slider = $('.d3-slider-handle')[0]
		$scope.slider.style.left = "0%";
		$scope.timePassed = 0;

		$timeout(function(){
			animateSlider(0);
		})
	});

	var animateSlider = function(to){
		if (to <= 100){
			$timeout(function(){
				$scope.moveSlider(to);
				animateSlider(to+1);
			}, 25);
		}
	}

	$scope.scrollMin = null;
	$scope.scrollMax = null;

	$scope.scrollTimer = null;

	$scope.scrollHandle = function(ele, last){
		if (last){
			console.log(ele.scrollTop);
		}
		var scrollMin = Math.floor($scope.lineCount * ele.scrollTop / ele.scrollHeight) + 1;
		var scrollMax = Math.floor($scope.lineCount * (ele.scrollTop+ele.clientHeight) / ele.scrollHeight);

		if ($scope.scrollMax === null){
			for (var i=1; i<scrollMin; i++){
				document.getElementById(String(i)).style['font-weight'] = "300";
			}
			for (var i=scrollMin; i<=scrollMax; i++){
				var ele = document.getElementById(String(i));
				if (!ele){
					return;
				}
				ele.style['font-weight'] = "600";
			}
			for (var i=scrollMax + 1; i<$scope.lineCount; i++){
				document.getElementById(String(i)).style['font-weight'] = "300";
			}
		} else {
			for (var i=$scope.scrollMin; i<scrollMin; i++){
				document.getElementById(String(i)).style['font-weight'] = "300";
			}
			var j = scrollMin < $scope.scrollMin ? scrollMin : Math.max(scrollMin, $scope.scrollMax);
			var k = scrollMax > $scope.scrollMax ? scrollMax : Math.min(scrollMax, $scope.scrollMin);
			for (var i=j; i<k; i++){
				var ele = document.getElementById(String(i));
				if (!ele){
					console.log(i);
				}
				ele.style['font-weight'] = "600";
			}
			for (var i=scrollMax; i<$scope.scrollMax; i++){
				document.getElementById(String(i)).style['font-weight'] = "300";
			}
		}
		$scope.scrollMin = scrollMin;
		$scope.scrollMax = scrollMax;
	}

	function lineColor(line){
		var alpha = String($scope.frequencies[line]/$scope.max_frequency);
		return "rgba(77,254,166,"+alpha+")";
	}

	$scope.lineStyle = function(line){
		return {"background-color":lineColor(line)}
	}

	$scope.hoverHandle = function(line){
		d = {key:line}
		mouseoverNode.call(document.getElementById(String(line)), d);
	}
	$scope.hoverHandleOut = function(line){
		d = {key:line}
		mouseoutNode.call(document.getElementById(String(line)), d);
	}

	$scope.execute = function(line){
		$scope.frequencies[line] += 1;
		$scope.max_frequency = Math.max($scope.max_frequency, $scope.frequencies[line]);
	}

	$scope.moveSlider = function(to){
		slide(null, Math.ceil(to/100*code.total));
		$scope.slider.style.left = String(to)+"%";
	}

}];