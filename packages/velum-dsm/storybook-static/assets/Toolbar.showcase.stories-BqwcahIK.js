import{j as e,H as o,k as t,T as s,l as i}from"./iframe-v_xVpIIQ.js";import{S as d,a as p,b as c}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const h={title:"Components/Actions/Toolbar"},a={render:()=>e.jsx(d,{maxWidth:"1100px",children:e.jsx(p,{children:e.jsx(c,{label:"Mixed Controls",description:"Toolbar with select, input, and textarea",minHeight:"260px",children:e.jsxs(o,{children:[e.jsxs("label",{style:{display:"grid",gap:"8px"},children:["Source",e.jsxs(t,{defaultValue:"translator",children:[e.jsx("option",{value:"translator",children:"Translator"}),e.jsx("option",{value:"formatter",children:"Formatter"})]})]}),e.jsxs("label",{style:{display:"grid",gap:"8px"},children:["Sheet",e.jsxs(t,{defaultValue:"modern",children:[e.jsx("option",{value:"modern",children:"Modern Lexicon"}),e.jsx("option",{value:"fantasy",children:"Fantasy Bestiary"})]})]}),e.jsxs("label",{style:{display:"grid",gap:"8px"},children:["Search",e.jsx(s,{defaultValue:"Ashmarked"})]}),e.jsxs("label",{style:{display:"grid",gap:"8px"},children:["Notes",e.jsx(i,{defaultValue:"Toolbar children can be any form controls.",rows:4})]})]})})})})};var n,r,l;a.parameters={...a.parameters,docs:{...(n=a.parameters)==null?void 0:n.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1100px">
      <StateMatrix>
        <StateCase label="Mixed Controls" description="Toolbar with select, input, and textarea" minHeight="260px">
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
              Sheet
              <SelectInput defaultValue="modern">
                <option value="modern">Modern Lexicon</option>
                <option value="fantasy">Fantasy Bestiary</option>
              </SelectInput>
            </label>
            <label style={{
            display: "grid",
            gap: "8px"
          }}>
              Search
              <TextInput defaultValue="Ashmarked" />
            </label>
            <label style={{
            display: "grid",
            gap: "8px"
          }}>
              Notes
              <TextArea defaultValue="Toolbar children can be any form controls." rows={4} />
            </label>
          </Toolbar>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(l=(r=a.parameters)==null?void 0:r.docs)==null?void 0:l.source}}};const y=["Showcase"];export{a as Showcase,y as __namedExportsOrder,h as default};
