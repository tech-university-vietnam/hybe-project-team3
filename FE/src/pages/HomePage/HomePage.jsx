import React from "react";
import { Greeting } from 'components/Greeting/Greeting'
import className from "./HomePage.css"

export const HomePage = () => (
  <div className={className.textAlign}>
    <Greeting />
  </div>
)

