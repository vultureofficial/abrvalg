unit Unit1;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, SynEdit,
  SynHighlighterAny, ExtCtrls, ShellCtrls;

type

  { TForm1 }

  TForm1 = class(TForm)
    SynHighlighter: TSynAnySyn;
    SynEdit1: TSynEdit;
  private

  public

  end;

var
  Form1: TForm1;

implementation

{$R *.lfm}

end.

