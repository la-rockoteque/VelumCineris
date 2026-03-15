import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{S as l,a as m,b as i,D as n}from"./_helpers-N5hE6fGh.js";import{u as s,v as r}from"./VelumProvider-Cnx-m3OC.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const x={title:"Patterns/Section"},t={render:()=>e.jsx(l,{children:e.jsxs(m,{children:[e.jsx(i,{label:"Nested",description:"Section containing multiple subsections",minHeight:"260px",children:e.jsxs(s,{title:"Compendium Section",subtitle:"Top-level grouping for related content blocks.",children:[e.jsx(r,{title:"Primary Fields",children:e.jsx(n,{children:"Fields, summaries, and nested patterns can all live inside a section."})}),e.jsx(r,{title:"Secondary Fields",children:e.jsx(n,{children:"Sections are useful when the grouping matters more than a framed surface."})})]})}),e.jsx(i,{label:"Simple",description:"Section without nested hierarchy",minHeight:"180px",children:e.jsx(s,{title:"Simple Section",children:e.jsx(n,{children:"Use the section pattern when structure matters more than chrome."})})})]})})};var o,a,c;t.parameters={...t.parameters,docs:{...(o=t.parameters)==null?void 0:o.docs,source:{originalSource:`{
  render: () => <StoryFrame>
      <StateMatrix>
        <StateCase label="Nested" description="Section containing multiple subsections" minHeight="260px">
          <Section title="Compendium Section" subtitle="Top-level grouping for related content blocks.">
            <Subsection title="Primary Fields">
              <DemoBlock>Fields, summaries, and nested patterns can all live inside a section.</DemoBlock>
            </Subsection>
            <Subsection title="Secondary Fields">
              <DemoBlock>Sections are useful when the grouping matters more than a framed surface.</DemoBlock>
            </Subsection>
          </Section>
        </StateCase>
        <StateCase label="Simple" description="Section without nested hierarchy" minHeight="180px">
          <Section title="Simple Section">
            <DemoBlock>Use the section pattern when structure matters more than chrome.</DemoBlock>
          </Section>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(c=(a=t.parameters)==null?void 0:a.docs)==null?void 0:c.source}}};const b=["Showcase"];export{t as Showcase,b as __namedExportsOrder,x as default};
