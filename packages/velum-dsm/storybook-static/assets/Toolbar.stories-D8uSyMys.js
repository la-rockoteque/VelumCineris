import{H as n,j as e,k as o,T as s}from"./iframe-v_xVpIIQ.js";import{S as p}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const c={title:"Components/Actions/Toolbar",component:n},r={render:()=>e.jsx(p,{maxWidth:"960px",children:e.jsxs(n,{children:[e.jsxs("label",{style:{display:"grid",gap:"8px"},children:["Source",e.jsxs(o,{defaultValue:"translator",children:[e.jsx("option",{value:"translator",children:"Translator"}),e.jsx("option",{value:"formatter",children:"Formatter"})]})]}),e.jsxs("label",{style:{display:"grid",gap:"8px"},children:["Filter",e.jsx(s,{defaultValue:"Archive"})]})]})})};var t,a,l;r.parameters={...r.parameters,docs:{...(t=r.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="960px">
      <Toolbar>
        <label style={{
        display: "grid",
        gap: "8px"
      }}>
          Source
          <SelectInput defaultValue="translator">
            <option value="translator">Translator</option>
            <option value="formatter">Formatter</option>
          </SelectInput>
        </label>
        <label style={{
        display: "grid",
        gap: "8px"
      }}>
          Filter
          <TextInput defaultValue="Archive" />
        </label>
      </Toolbar>
    </StoryFrame>
}`,...(l=(a=r.parameters)==null?void 0:a.docs)==null?void 0:l.source}}};const m=["Default"];export{r as Default,m as __namedExportsOrder,c as default};
