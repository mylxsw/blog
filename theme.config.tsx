import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: <span>mylxsw's Blog</span>,
  project: {
    link: 'https://github.com/mylxsw',
  },
  footer: {
    text: 'CC BY-NC 4.0 ' + new Date().getFullYear() + ' © mylxsw | Powered by Nextra',
  },
  editLink: {
    component: null,
  },
  feedback: {
    content: null,
  },
  
}

export default config
