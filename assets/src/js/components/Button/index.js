import React from 'react'
import './index.less'

const Button = ({ text, height, width, color, onClickFunction }) => {
  return (
    <div className="button--wrapper" style={{height: height, width: width, backgroundColor: color}} onClick={() => onClickFunction()}>
      <span>{text}</span>
    </div>
  )
}
export default Button