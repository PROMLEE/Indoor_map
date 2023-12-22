import React from "react";
import styled from "styled-components";
import Contents from "./Captions";
import { useSelector } from "react-redux";

export default function EditCaption() {
  const Data = useSelector((state) => state.state.data);
  const Floor = useSelector((state) => state.state.floor);
  const Buildingname = useSelector((state) => state.state.buildingname);
  const api = useSelector((state) => state.state.url);
  var realImg = `${api}/source/${Buildingname}_${Floor}`;
  var maskImg = `${api}/mask/${Buildingname}_${Floor}?time=${new Date().getTime()}`;

  return (
    <div>
      <Appform>
        {Data.map((item) => {
          if (item.id !== -2 && item.id !== 1) {
            return (
              <Contents id={item.id} caption={item.caption} key={item.id} />
            );
          } else {
            return null;
          }
        })}
      </Appform>
      <Images>
        <Maskimg src={maskImg} />
        <Maskimg src={realImg} />
      </Images>
    </div>
  );
}
const Appform = styled.div`
  background-color: #bbbbbb29;
  width: 60%;
  overflow: scroll;
  height: 200px;
  border-radius: 5%;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
  padding: 20px;
  padding-left: 50px;
  gap: 20px;
  border: black;
`;
const Images = styled.div`
  display: flex;
  margin-top: 40px;
  justify-content: center;
  align-items: center;
  gap: 10px;
`;
const Maskimg = styled.img`
  width: 40vw;
  height: 40vw;
  &:hover {
    width: 60vw;
    height: 60vw;
  }
`;
