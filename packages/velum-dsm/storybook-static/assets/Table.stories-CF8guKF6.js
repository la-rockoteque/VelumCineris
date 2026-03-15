import{q as l,j as o,p as s}from"./iframe-v_xVpIIQ.js";import{S as t}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const p={title:"Components/Table",component:l,args:{columns:[],rows:[],onRowClick:()=>{}}},m=[{name:"Magic Missile",level:"1",school:"Evocation"},{name:"Shield",level:"1",school:"Abjuration"},{name:"Counterspell",level:"3",school:"Abjuration"}],e={render:()=>o.jsx(t,{maxWidth:"980px",children:o.jsx(s,{children:o.jsx(l,{rows:m,onRowClick:()=>{},columns:[{key:"name",header:"Name"},{key:"level",header:"Level",width:"90px"},{key:"school",header:"School"}]})})})};var a,r,n;e.parameters={...e.parameters,docs:{...(a=e.parameters)==null?void 0:a.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <TableWrap>
        <Table rows={rows} onRowClick={() => undefined} columns={[{
        key: "name",
        header: "Name"
      }, {
        key: "level",
        header: "Level",
        width: "90px"
      }, {
        key: "school",
        header: "School"
      }]} />
      </TableWrap>
    </StoryFrame>
}`,...(n=(r=e.parameters)==null?void 0:r.docs)==null?void 0:n.source}}};const h=["Default"];export{e as Default,h as __namedExportsOrder,p as default};
