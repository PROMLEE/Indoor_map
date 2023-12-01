import styled from "styled-components";

export default function Contents({ id, caption }) {
  return (
    <Wrapper>
      <Info>
        <Namebox>{id}: </Namebox>
        <Date value={caption} />
      </Info>
    </Wrapper>
  );
}

const Wrapper = styled.span`
  position: relative;
  border-color: black solid 1px;
`;
const Info = styled.div`
  width: 150px;
  height: 30px;
  display: flex;
  justify-content: center;
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
  width: 100px;
  font-size: 13px;
  border: solid, 1px;
`;
