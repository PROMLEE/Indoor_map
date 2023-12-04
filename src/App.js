import Main from "./Components/Main.jsx";
import { BrowserRouter } from "react-router-dom";
export default function App() {
  document.body.style.margin = 0;
  return (
    <div>
      <BrowserRouter>
        <Main></Main>
      </BrowserRouter>
    </div>
  );
}
