#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2011 Shuttleworth Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
SchoolTool flourish pages.
"""
from zope.interface import Interface
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.interface import implements
from zope.publisher.browser import BrowserPage
from zope.traversing.api import getParent

from schooltool.app.browser.content import IContentProviders
from schooltool.common.inlinept import InlineViewPageTemplate
from schooltool.skin.flourish.viewlet import Viewlet, ViewletManager
from schooltool.skin.flourish import interfaces


class Page(BrowserPage):
    implements(interfaces.IPage)

    title = None
    subtitle = None

    template = ViewPageTemplateFile('templates/main.pt')
    page_template = ViewPageTemplateFile('templates/page.pt')
    content_template = None

    @Lazy
    def providers(self):
        providers = getMultiAdapter(
            (self.context, self.request, self),
            IContentProviders)
        return providers

    def update(self):
        pass

    def render(self, *args, **kw):
        return self.template(*args, **kw)

    def __call__(self, *args, **kw):
        self.update()
        result = self.render(*args, **kw)
        return result


class ExpandedPage(Page):
    page_template = ViewPageTemplateFile('templates/page_expanded.pt')


class Refine(Viewlet):

    template = InlineViewPageTemplate('''
      <div class="header"
           tal:condition="view/title"
           tal:content="view/title">
        [ Filter title ]
      </div>
      <div class="body" tal:content="structure view/body_template">
        [ options ]
      </div>
    ''')
    body_template = None
    title = None


class Content(Viewlet):

    template = InlineViewPageTemplate('''
      <div class="header"
           tal:define="actions context/schootlool:content/actions"
           tal:condition="actions"
           tal:content="structure actions">
        [action] [buttons]
      </div>
      <div class="body" tal:content="structure view/body_template">
        [ The content itself ]
      </div>
    ''')
    body_template = None


class Related(Viewlet):

    template = InlineViewPageTemplate('''
      <div class="header"
           tal:condition="view/title"
           tal:content="view/title">
        [ Title ]
      </div>
      <div class="body" tal:content="structure view/body_template">
        [ Related info ]
      </div>
    ''')

    body_template = None
    title = None


class ListNavigationManager(ViewletManager):
    template = InlineViewPageTemplate("""
        <ul class="navigation">
          <li tal:repeat="item view/items"
              tal:attributes="class item/class"
              tal:content="structure item/viewlet">
          </li>
        </ul>
    """)

    active_viewlet = None

    @property
    def items(self):
        result = []
        active = self.active_viewlet
        for viewlet in self.viewlets:
            result.append({
                'class': viewlet.__name__ == active and 'active' or None,
                'viewlet': viewlet,
                })
        return result

    @property
    def active(self):
        name = self.active_viewlet
        return(name and name in self.order)


def getParentActiveViewletName(context, request, view, manager):
    parent = getParent(context)
    name = getMultiAdapter(
        (parent, request, view),
        interfaces.IActiveViewletName)
    return name


class HeaderNavigationManager(ViewletManager):

    @Lazy
    def active_viewlet(self):
        name = queryMultiAdapter(
            (self.context, self.request, self.view),
            interfaces.IActiveViewletName,
            default=None)
        return name


class PageNavigationManager(ListNavigationManager):

    @property
    def active_viewlet(self):
        return getattr(self.view, '__name__', None)

    def render(self, *args, **kw):
        if not self.active:
            return ''
        return ListNavigationManager.render(*args, **kw)


class IHTMLHeadManager(interfaces.IViewletManager):
    pass


class IHeaderNavigationManager(interfaces.IViewletManager):
    pass


class IPageNavigationManager(interfaces.IViewletManager):
    pass


class IPageRefineManager(interfaces.IViewletManager):
    pass


class IPageContentManager(interfaces.IViewletManager):
    pass


class IContentActionsManager(interfaces.IViewletManager):
    pass


class IPageRelatedManager(interfaces.IViewletManager):
    pass


class LinkViewlet(Viewlet):
    template = InlineViewPageTemplate('''
    <a tal:attributes="href view/link" tal:content="view/title"></a>
    ''')

    render = lambda self, *a, **kw: self.template(*a, **kw)

    title = None

    @property
    def link(self):
        return None
