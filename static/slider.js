$(window).on('load', function() {
    console.log("loaded js");
    $("#slider").on('input',function() {
        console.log("year change!");
        $("#year").html("Year: " + this.value);
        $.get('/rainfall',
            { "year" : this.value },
            function (data) {
                console.log("got json");
                $("#rainfall").attr("src", data);
            },
            "text"
        );
    });
});
