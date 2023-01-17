void conv(const char *fname = "/mnt/windows/Uwintu/work/conversion/original/HemisphericPET1LayerPixelatedBGO_01MBq_1.root",
          const char *nname = "Singles")
{
  if (!fname || !(*fname) || !nname || !(*nname)) return; // just a precaution
  
  TFile *f = TFile::Open(fname, "READ");
  if ((!f) || f->IsZombie()) { delete f; return; } // just a precaution
  
  TTree *t; f->GetObject(nname, t);
  if (!t) { delete f; return; } // just a precaution
  
  t->SetScanField(0);
  ((TTreePlayer*)(t->GetPlayer()))->SetScanRedirect(true);
  ((TTreePlayer*)(t->GetPlayer()))->SetScanFileName("Singles.txt");
  t->Scan("*");

 // t->SaveAs("modify.txt");
  // t->SaveAs(TString::Format("%s.xml", nname));
  
  delete f; // no longer needed (automatically deletes "t")
}

