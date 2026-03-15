import{j as e,f as m,v as p}from"./iframe-v_xVpIIQ.js";import{S as x,a as c,b as a}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const S={title:"Components/DelimitedListField"};function s(i){const[l,d]=m.useState(i.initialValue);return e.jsx(p,{value:l,onChange:d,options:i.options})}const t={render:()=>e.jsx(x,{maxWidth:"1080px",children:e.jsxs(c,{columns:"1fr",children:[e.jsx(a,{label:"Suggested Values",description:"Editable rows with datalist suggestions",minHeight:"220px",children:e.jsx(s,{initialValue:"Fire, Cold",options:["Fire","Cold","Lightning","Poison"]})}),e.jsx(a,{label:"Blank List",description:"Begins with a single empty editable row",minHeight:"180px",children:e.jsx(s,{initialValue:""})})]})})};var n,o,r;t.parameters={...t.parameters,docs:{...(n=t.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1080px">
      <StateMatrix columns="1fr">
        <StateCase label="Suggested Values" description="Editable rows with datalist suggestions" minHeight="220px">
          <Example initialValue="Fire, Cold" options={["Fire", "Cold", "Lightning", "Poison"]} />
        </StateCase>
        <StateCase label="Blank List" description="Begins with a single empty editable row" minHeight="180px">
          <Example initialValue="" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(r=(o=t.parameters)==null?void 0:o.docs)==null?void 0:r.source}}};const C=["Showcase"];export{t as Showcase,C as __namedExportsOrder,S as default};
