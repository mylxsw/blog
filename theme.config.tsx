import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: <span>mylxsw's Blog</span>,
  project: {
    link: 'https://github.com/mylxsw',
  },
  footer: {
    text: new Date().getFullYear() + ' © by mylxsw | Powered by Nextra',
  },
  editLink: {
    component: null,
  },
  feedback: {
    content: null,
  },
}

export default config
