import React from 'react'
import './index.less'

const Header = ({ title }) => {
  return (
    <div className="header--wrapper">
      <h1>{title}</h1>
    </div>
  )
}
export default Header