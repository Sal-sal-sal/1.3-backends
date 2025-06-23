import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { ChatApp } from './components/ChatApp'
import { Route, Routes } from 'react-router'
function App() {

  return (
    <Routes>
      <Route path='/' element={<ChatApp />} ></Route>
    </Routes>
  )
}

export default App
