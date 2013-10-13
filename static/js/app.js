if (window.requirements && window.requirements.length > 0) {
    var app = angular.module('anting', window.requirements);
} else {
    var app = angular.module('anting', []);
}

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}]);


var Util = {}

// turns "mm:ss.sss" into seconds
Util.parseTime = function(timestring){
	if (timestring.indexOf(':') == -1){
		return parseFloat(timestring);
	}
	var timearray = timestring.split(':')
	return parseInt(timearray[0])*60+parseFloat(timearray[1])
}
Util.unParseTime = function(seconds, forceSign){
	var sign = "";
	if (seconds < 0) {
		seconds = 0-seconds;
		sign = "-";
	} else if (forceSign) {
		sign = "+";
	}
	var min = Math.floor(seconds/60)
	return sign + (min ? String(min) + ":" : "" )
		+ String((seconds % 60).toFixed(3))
}
Util.enableTab = function(id) {
    var el = document.getElementById(id);
    el.onkeydown = function(e) {
        if (e.keyCode === 9) { // tab was pressed

            // get caret position/selection
            var val = this.value,
                start = this.selectionStart,
                end = this.selectionEnd;

            // set textarea value to: text before caret + tab + text after caret
            this.value = val.substring(0, start) + '\t' + val.substring(end);

            // put caret at right position again
            this.selectionStart = this.selectionEnd = start + 1;

            // prevent the focus lose
            return false;
        }
    };
}