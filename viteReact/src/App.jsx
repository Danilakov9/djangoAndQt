import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Login from './pages/Login';
import Home from './pages/Home';
import Count from './pages/Count';
import { Provider } from 'react-redux';
import store from './store/store';
import 'antd/dist/reset.css';
function App() {

  return (
    <Provider store={store}>
      <Router>
        <Routes>
          <Route exact path='/' Component={Home} />
          <Route path='/count' Component={Count} />
          <Route path='/login' Component={Login} />
        </Routes>
      </Router>
    </Provider>
  )
}

export default App
