import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useDispatch } from "react-redux";
import { updateDataItem } from "../Redux/state";

export default function Contents({ id, caption, move_up, move_down }) {
  const backupmoveup = move_up;
  const backupmovedown = move_down;
  const [newup, setnewup] = useState();
  const [newdown, setnewdown] = useState();
  const [upvalue, setupvalue] = useState();
  const [downvalue, setdownvalue] = useState();
  const dispatch = useDispatch();

  useEffect(() => {
    setupvalue(move_up);
    setdownvalue(move_down);
    setnewup();
    setnewdown();
  }, [move_up, move_down]);

  const updateItem = () => {
    if (newup !== "" || newdown !== "")
      dispatch(updateDataItem(id, newup, newdown));
    else dispatch(updateDataItem(id, backupmoveup, backupmovedown));
  };

  return (
    <Wrapper>
      <Info>
        <Namebox>{id} </Namebox>
        <Namebox>{caption}: </Namebox>
        <Date
          placeholder={upvalue || ""}
          value={newup || ""}
          onChange={(e) => {
            setnewup(e.target.value);
          }}
          onBlur={updateItem}
        />
        <Date
          placeholder={downvalue || ""}
          value={newdown || ""}
          onChange={(e) => {
            setnewdown(e.target.value);
          }}
          onBlur={updateItem}
        />
      </Info>
    </Wrapper>
  );
}

const Wrapper = styled.span`
  position: relative;
  border-color: black solid 1px;
`;
const Info = styled.div`
  width: 300px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
`;
const Namebox = styled.div`
  font-size: 15px;
  padding-left: 20px;
  width: 50px;
  font-weight: bold;
  font-family: "굴림";
`;
const Date = styled.input`
  margin-left: 5px;
  width: 20px;
  font-size: 13px;
  border: solid, 1px;
`;
