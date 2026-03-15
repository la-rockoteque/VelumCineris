import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{P as o}from"./VelumProvider-Cnx-m3OC.js";import{S as s,a as c,b as r,D as a}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const B={title:"Patterns/PanelGrid"},n={render:()=>e.jsx(s,{maxWidth:"1100px",children:e.jsxs(c,{children:[e.jsx(r,{label:"Four Panels",description:"Balanced grid with equal cards",minHeight:"260px",children:e.jsxs(o,{$min:"200px",children:[e.jsx(a,{children:"Panel 1"}),e.jsx(a,{children:"Panel 2"}),e.jsx(a,{children:"Panel 3"}),e.jsx(a,{children:"Panel 4"})]})}),e.jsx(r,{label:"Narrow Min Width",description:"More aggressive auto-fit layout",minHeight:"260px",children:e.jsxs(o,{$min:"140px",children:[e.jsx(a,{children:"A"}),e.jsx(a,{children:"B"}),e.jsx(a,{children:"C"}),e.jsx(a,{children:"D"}),e.jsx(a,{children:"E"})]})})]})})};var i,l,t;n.parameters={...n.parameters,docs:{...(i=n.parameters)==null?void 0:i.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1100px">
      <StateMatrix>
        <StateCase label="Four Panels" description="Balanced grid with equal cards" minHeight="260px">
          <PanelGrid $min="200px">
            <DemoBlock>Panel 1</DemoBlock>
            <DemoBlock>Panel 2</DemoBlock>
            <DemoBlock>Panel 3</DemoBlock>
            <DemoBlock>Panel 4</DemoBlock>
          </PanelGrid>
        </StateCase>
        <StateCase label="Narrow Min Width" description="More aggressive auto-fit layout" minHeight="260px">
          <PanelGrid $min="140px">
            <DemoBlock>A</DemoBlock>
            <DemoBlock>B</DemoBlock>
            <DemoBlock>C</DemoBlock>
            <DemoBlock>D</DemoBlock>
            <DemoBlock>E</DemoBlock>
          </PanelGrid>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(t=(l=n.parameters)==null?void 0:l.docs)==null?void 0:t.source}}};const D=["Showcase"];export{n as Showcase,D as __namedExportsOrder,B as default};
