import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useDispatch } from "react-redux";
import { updateUpdown } from "../Redux/state";

export default function Contents({ id, caption, move_up, move_down }) {
  var backupmoveup = 0;
  var backupmovedown = 0;
  if (move_up) {
    backupmoveup = move_up;
  }
  if (move_down) {
    backupmovedown = move_down;
  }
  const [newup, setnewup] = useState();
  const [newdown, setnewdown] = useState();
  const [upvalue, setupvalue] = useState();
  const [downvalue, setdownvalue] = useState();
  const dispatch = useDispatch();

  useEffect(() => {
    console.log(move_up, move_down);
    setupvalue(move_up);
    setdownvalue(move_down);
    setnewup();
    setnewdown();
  }, [move_up, move_down]);

  const updateItem = () => {
    console.log(newup, newdown);

    if (newup && newdown) dispatch(updateUpdown(id, caption, newup, newdown));
    else if (newup) {
      dispatch(updateUpdown(id, caption, newup, backupmovedown));
    } else if (newdown) {
      dispatch(updateUpdown(id, caption, backupmoveup, newdown));
    } else dispatch(updateUpdown(id, caption, backupmoveup, backupmovedown));
  };

  return (
    <Wrapper>
      <Info>
        <Namebox>{id} </Namebox>
        <Nameboxcap>{caption}: </Nameboxcap>
        <Date
          placeholder={upvalue || "0"}
          value={newup || ""}
          onChange={(e) => {
            setnewup(e.target.value);
          }}
          onBlur={updateItem}
        />
        <Date
          placeholder={downvalue || "0"}
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
  width: 20px;
  font-weight: bold;
  font-family: "굴림";
`;
const Nameboxcap = styled.div`
  font-size: 15px;
  padding-left: 20px;
  width: 100px;
  font-weight: bold;
  font-family: "굴림";
`;
const Date = styled.input`
  margin-left: 5px;
  width: 20px;
  font-size: 13px;
  border: solid, 1px;
`;
