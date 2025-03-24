function displayPosts(posts){
    //empty old data
    $(".post-feed").empty()

    //insert all new data
    $.each(posts, function(i, datum){
        let new_post= $("<div>"+datum["name"]+"</div>")
        $("#people_container").append(new_name)
    })
}

$(document).ready(function(){
    //when the page loads, display all the names
    displayPosts(posts)                        
})