import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'
import { BaiduStatistics } from './components/statistics'

const config: DocsThemeConfig = {
  logo: <span>mylxsw's Blog</span>,
  project: {
    link: 'https://github.com/mylxsw',
  },
  head: <BaiduStatistics />,
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
