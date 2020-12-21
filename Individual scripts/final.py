from generate_sitemap import createsitemap
createsitemap()

from download_HTML import downloadHTMLfiles
downloadHTMLfiles()

from generate_static_links import generatestaticlinks
generatestaticlinks()

from download_STATIC import downloadSTATICfiles
downloadSTATICfiles()




from handle_internal_href import handleinternalhref
handleinternalhref()

from update_HTML import updateHTML
updateHTML()

print('_'*100)