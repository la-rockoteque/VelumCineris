import{j as t}from"./jsx-runtime-Bll8AAhy.js";import{A as n,b as e}from"./VelumProvider-Cnx-m3OC.js";import{S as l,a as c,b as r}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const h={title:"Patterns/ActionRow"},a={render:()=>t.jsx(l,{children:t.jsxs(c,{children:[t.jsx(r,{label:"Standard",description:"Common multi-action row",children:t.jsxs(n,{children:[t.jsx(e,{$variant:"primary",children:"Save"}),t.jsx(e,{children:"Reload"}),t.jsx(e,{children:"Validate"}),t.jsx(e,{$variant:"ghost",children:"Reset"})]})}),t.jsx(r,{label:"Wrapping",description:"Long labels still wrap cleanly",minHeight:"96px",children:t.jsxs(n,{children:[t.jsx(e,{$variant:"primary",children:"Publish to Google Docs"}),t.jsx(e,{children:"Generate Homebrewery Preview"})]})})]})})};var o,i,s;a.parameters={...a.parameters,docs:{...(o=a.parameters)==null?void 0:o.docs,source:{originalSource:`{
  render: () => <StoryFrame>
      <StateMatrix>
        <StateCase label="Standard" description="Common multi-action row">
          <ActionRow>
            <Button $variant="primary">Save</Button>
            <Button>Reload</Button>
            <Button>Validate</Button>
            <Button $variant="ghost">Reset</Button>
          </ActionRow>
        </StateCase>
        <StateCase label="Wrapping" description="Long labels still wrap cleanly" minHeight="96px">
          <ActionRow>
            <Button $variant="primary">Publish to Google Docs</Button>
            <Button>Generate Homebrewery Preview</Button>
          </ActionRow>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(s=(i=a.parameters)==null?void 0:i.docs)==null?void 0:s.source}}};const S=["Showcase"];export{a as Showcase,S as __namedExportsOrder,h as default};
