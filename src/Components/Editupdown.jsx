import React from "react";
import styled from "styled-components";
import Contents from "./Updowns";
import { useSelector } from "react-redux";

export default function EditCaption() {
  const Data = useSelector((state) => state.state.data);
  const Floor = useSelector((state) => state.state.floor);
  const uFloor = useSelector((state) => state.state.ufloor);
  const dFloor = useSelector((state) => state.state.dfloor);
  const Buildingname = useSelector((state) => state.state.buildingname);
  const api = useSelector((state) => state.state.url);
  var maskImgdown = `${api}/mask/${Buildingname}_${dFloor}?time=${new Date().getTime()}`;
  var maskImg = `${api}/mask/${Buildingname}_${Floor}?time=${new Date().getTime()}`;
  var maskImgup = `${api}/mask/${Buildingname}_${uFloor}?time=${new Date().getTime()}`;

  return (
    <div>
      <Appform>
        {Data.map((item) => {
          if (
            item.id !== -2 &&
            item.id !== 1 &&
            ["엘리베이터", "계단", "elevator", "stair"].includes(item.caption)
          ) {
            return (
              <Contents
                id={item.id}
                caption={item.caption}
                move_up={item.move_up}
                move_down={item.move_down}
                key={item.id}
              />
            );
          } else {
            return null;
          }
        })}
      </Appform>
      <Images>
        <Maskimg src={maskImgdown} />
        <Maskimg src={maskImg} />
        <Maskimg src={maskImgup} />
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
  justify-content: space-between;
  align-items: center;
  /* flex-wrap: wrap; */
  /* gap: 10px; */
  flex: 1 1 1;
`;
const Maskimg = styled.img`
  /* align-items: center; */
  width: 33vw;
  /* object-fit: cover; */
  &:hover {
    width: 50vw;
  }
`;
