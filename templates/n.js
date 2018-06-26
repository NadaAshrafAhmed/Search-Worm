chrome.storage.local.get('offlinePages',function(pages){
 console.log(pages['offlinePages']);
});

function save_remove(tablink)
{
    var link = document.getElementById('download')
    if(link.innerHTML =="Save Page")
    {
        console.log("download");
        chrome.storage.local.get('offlinePages',function(pages){

            if(pages['offlinePages'])
            {
                pages['offlinePages'].push({'url':tablink,'html':"<html><body><a href='"+tablink+"'>page</a></body></html>"});
                chrome.storage.local.set({'offlinePages':pages['offlinePages']});
                console.log(pages['offlinePages']);
                link.innerHTML ="Delete Page";
            }

        });

    }
    if(link.innerHTML =="Delete Page")
    {
        console.log('remove');
        chrome.storage.local.get('offlinePages',function(pages){
            if(pages['offlinePages'])
            {
                for(var i=0;i<pages['offlinePages'].length;i++)
                {
                    if(pages['offlinePages'][i]['url']==tablink)
                    {
                        pages['offlinePages'].splice(i,1);
                        chrome.storage.local.set({'offlinePages':pages['offlinePages']});
                        document.getElementById('download').innerHTML ="Delete Page";
                        console.log(pages['offlinePages']);
                        link.innerHTML ="Save Page";
                        break;
                    }
                }
            }
        });
    }
}
function download(tablink)
{

    console.log("download");
    chrome.storage.local.get('offlinePages',function(pages){

        if(pages['offlinePages'])
        {
//                var x=pages['offlinePages'];
            pages['offlinePages'].push({'url':tablink,'html':"<html><body><a href='"+tablink+"'>page</a></body></html>"});
            chrome.storage.local.set({'offlinePages':pages['offlinePages']});
            console.log(pages['offlinePages']);
            convert(tablink);
        }

    });

}
function remove(tablink)
{

    console.log('remove');
    chrome.storage.local.get('offlinePages',function(pages){
        if(pages['offlinePages'])
        {
            for(var i=0;i<pages['offlinePages'].length;i++)
            {
                if(pages['offlinePages'][i]['url']==tablink)
                {
                    pages['offlinePages'].splice(i,1);
                    chrome.storage.local.set({'offlinePages':pages['offlinePages']});
                    document.getElementById('download').innerHTML ="Delete Page";
                    console.log(pages['offlinePages']);
                    convert(tablink);
                    break;
                }
            }
        }
    });

}
chrome.tabs.getSelected(null, function (tab) {

    var tablink = tab.url;
    console.log(tablink);
    chrome.storage.local.get('offlinePages',function(pages){
        var downloaded=false;
        if(pages['offlinePages'])
        {
            for(var i=0;i<pages['offlinePages'].length;i++)
            {
                if(pages['offlinePages'][i]['url']==tablink)
                {
                    var link = document.getElementById('download')
                    link.innerHTML ="Delete Page";
                    downloaded=true;
                    link.addEventListener('click', function() {
                        save_remove(tablink);
                    });
                    break;
                }
            }
        }
        else
        {
            chrome.storage.local.set({'offlinePages':[]});
        }


        if(!downloaded)
        {
            var link = document.getElementById('download');
            link.innerHTML ="Save Page";
            link.addEventListener('click', function() {
                save_remove(tablink);
            });
        }
    });
});