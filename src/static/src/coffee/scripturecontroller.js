window.firstTime = true;
window.toggleCommentForm = function(verseId) {
	if(firstTime){
		$( "#commentFormHolder" ).append( getContentFormString(verseId, 23) );
		$( "#defaultCommentForm").hide();
		commentFormVisible = false;
		firstTime = false;
	}

	if(commentFormVisible){
		$('#defaultCommentForm').slideUp();
	}else{
		// alert("dfds");
		$('#defaultCommentForm').slideDown();
	}
	commentFormVisible = !commentFormVisible;
}

window.getContentFormString = function(verseId, inReplyToCommentId){
	formStr = '<form class="form" id="defaultCommentForm" method="POST" action="/addComment">'+
				'<textarea class="form-control" rows="3" name="commentBody" placeholder="Add your comment here...">'+
				'</textarea><br>'+
				'<input type="text" class="form-control" name="tags" placeholder="Add tags like: faith, hope, charity, etc"><br>'+
				'<div class="radio-inline">'+
			  		'<label><input type="radio" name="commentType" id="comment" value="comment" checked> comment </label>'+
				'</div>'+
				'<div class="radio-inline">'+
			  		'<label><input type="radio" name="commentType" id="question" value="question" checked> question </label>'+
				'</div>'+
				'<div class="radio-inline">'+
					'<label><input type="radio" name="commentType" id="crossreference" value="crossreference"> cross reference </label>'+
				'</div>'+
				'<input type="hidden" name="verseId" value='+verseId+'>'+
				'<input type="hidden" name="inReplyToCommentId" value='+inReplyToCommentId+'>'+
				'<button type="submit" class="btn btn-success">'+
				    'Submit'+
				 '</button>'+
				'</form>';
	return formStr;
}

// the on ready function
$(document).ready(function() {
	
	// toggleCommentForm();
	
	// $( "commentFormHolder" ).append( getContentFormString() );
});
