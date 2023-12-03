import Editor from "./Components/Editor.jsx";
import { BrowserRouter } from "react-router-dom";
export default function App() {
  document.body.style.margin = 0;
  return (
    <div>
      <BrowserRouter>
        <Editor></Editor>
      </BrowserRouter>
    </div>
  );
}
