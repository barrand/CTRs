window.showCommentForm = function() {
	if(commentFormVisible){
		$('#addCommentForm').slideUp();
	}else{
		$('#addCommentForm').slideDown();
	}
	commentFormVisible = !commentFormVisible;
}

// the on ready function
$(document).ready(function() {
	$('#addCommentForm').hide();
	commentFormVisible = false;
	

});
