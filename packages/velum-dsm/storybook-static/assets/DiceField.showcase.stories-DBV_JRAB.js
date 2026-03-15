import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{r as c}from"./index-hZsgmmNh.js";import{e as p}from"./VelumProvider-Cnx-m3OC.js";import{S as m,a as x,b as i}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const y={title:"Components/DiceField"};function a(s){const[o,d]=c.useState(s.initialValue);return e.jsx(p,{value:o,onChange:d,diceTypes:s.diceTypes})}const t={render:()=>e.jsx(m,{maxWidth:"980px",children:e.jsxs(x,{children:[e.jsx(i,{label:"Standard",description:"Classic hit dice expression",minHeight:"120px",children:e.jsx(a,{initialValue:"5d10+10"})}),e.jsx(i,{label:"Blank",description:"Starts empty until the user composes a value",minHeight:"120px",children:e.jsx(a,{initialValue:""})}),e.jsx(i,{label:"Custom Dice Set",description:"Allows non-default dice sizes",minHeight:"120px",children:e.jsx(a,{initialValue:"2d3+1",diceTypes:[3,4,6,8,10,12]})})]})})};var n,r,l;t.parameters={...t.parameters,docs:{...(n=t.parameters)==null?void 0:n.docs,source:{originalSource:`{
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
}`,...(l=(r=t.parameters)==null?void 0:r.docs)==null?void 0:l.source}}};const F=["Showcase"];export{t as Showcase,F as __namedExportsOrder,y as default};
