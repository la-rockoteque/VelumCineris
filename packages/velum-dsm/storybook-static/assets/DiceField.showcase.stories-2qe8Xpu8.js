import{j as e,f as c,D as p}from"./iframe-v_xVpIIQ.js";import{S as m,a as x,b as a}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const C={title:"Components/DiceField"};function i(s){const[o,d]=c.useState(s.initialValue);return e.jsx(p,{value:o,onChange:d,diceTypes:s.diceTypes})}const t={render:()=>e.jsx(m,{maxWidth:"980px",children:e.jsxs(x,{children:[e.jsx(a,{label:"Standard",description:"Classic hit dice expression",minHeight:"120px",children:e.jsx(i,{initialValue:"5d10+10"})}),e.jsx(a,{label:"Blank",description:"Starts empty until the user composes a value",minHeight:"120px",children:e.jsx(i,{initialValue:""})}),e.jsx(a,{label:"Custom Dice Set",description:"Allows non-default dice sizes",minHeight:"120px",children:e.jsx(i,{initialValue:"2d3+1",diceTypes:[3,4,6,8,10,12]})})]})})};var n,l,r;t.parameters={...t.parameters,docs:{...(n=t.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Standard" description="Classic hit dice expression" minHeight="120px">
          <ExampleField initialValue="5d10+10" />
        </StateCase>
        <StateCase label="Blank" description="Starts empty until the user composes a value" minHeight="120px">
          <ExampleField initialValue="" />
        </StateCase>
        <StateCase label="Custom Dice Set" description="Allows non-default dice sizes" minHeight="120px">
          <ExampleField initialValue="2d3+1" diceTypes={[3, 4, 6, 8, 10, 12]} />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(r=(l=t.parameters)==null?void 0:l.docs)==null?void 0:r.source}}};const j=["Showcase"];export{t as Showcase,j as __namedExportsOrder,C as default};
