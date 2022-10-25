import logo from './logo.svg';
import { GET_UNUSED } from './Queries';
import { useQuery } from '@apollo/client';
import LatestComment from './Messages/Messages';

const App = () => {
  const query = useQuery(GET_UNUSED);

  return(
  <div>
    <h1>Page title</h1>
    <img src={logo} height={100} alt="Alt logo" />
    <LatestComment />
  </div>
  )
}

export default App;
