import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: <span>mylxsw's Blog</span>,
  project: {
    link: 'https://github.com/mylxsw',
  },
  head: () => (
    <>
      <meta name="baidu-site-verification" content="code-from-baidu" />
      <script
        dangerouslySetInnerHTML={{
          __html: `
            var _hmt = _hmt || [];
            (function() {
              var hm = document.createElement("script");
              hm.src = "https://hm.baidu.com/hm.js?c77e5a3ef513ef219e1e4cbfa98a950e";
              var s = document.getElementsByTagName("script")[0];
              s.parentNode.insertBefore(hm, s);
            })();
          `
        }}
      />
      <script 
        async 
        src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6795823110480470" 
        crossOrigin="anonymous"
      />
    </>
  ),
  footer: {
    text: 'CC BY-NC 4.0 ' + new Date().getFullYear() + ' © mylxsw | Powered by Nextra',
  },
  editLink: {
    component: null,
  },
  feedback: {
    content: null,
  }
}

export default config
