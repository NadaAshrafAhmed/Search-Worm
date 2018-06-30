function DeletePage(tablink,fun)
{
    console.log('deleting...');
    chrome.storage.local.get('offlinePages', function (pages) {
        if (pages['offlinePages']) {
            for (var i = 0; i < pages['offlinePages'].length; i++) {
                if (pages['offlinePages'][i]['url'] == tablink) {
                    pages['offlinePages'].splice(i, 1);
                    chrome.storage.local.set({'offlinePages': pages['offlinePages']});
                    fun("Save Page")
                    break;
                }
            }
        }
    });
}