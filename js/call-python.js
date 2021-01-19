
// call python-script
function goPython()
{
    $.ajax({
        url: "feature_extraction.py " + file.name + " 3",
        context: document.body
        }).done(function() {
            Output('finished python script');;
        });
}